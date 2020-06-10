import asyncio
from aiofile import AIOFile, Writer, Reader
from typing import Callable, Optional
from pathlib import Path

OptionalFunction = Optional[Callable]

class AsyncCopyFileObj():
    def __init__(self, progress_callback: OptionalFunction = None,
                 finish_callback: OptionalFunction = None,
                 cancelled_callback: OptionalFunction = None,
                 current_file_changed_callback: OptionalFunction = None,
                 from_to_dict: dict = {},
                 chunk_size: int = 1024*1024):
        self.from_to_dict = from_to_dict
        self.progress_callback = progress_callback
        self.finish_callback = finish_callback
        self.cancelled_callback = cancelled_callback
        self.current_file_changed = current_file_changed_callback
        self.chunk_size = chunk_size
        self.progress = 0
        self.max_progress = self.__get_max_progress()

    def add_file(self, file_from, file_to):
        if Path(file_from).is_file():
            self.from_to_dict[file_from] = file_to
            self.max_progress += Path(file_from).stat().st_size
        else:
            raise Exception('file not found')

    def __check_all_file_exists(self):
        return all([Path(file).is_file() for file in self.from_to_dict.keys()])

    def __get_max_progress(self):
        return sum([Path(file).stat().st_size for file in self.from_to_dict.keys()])

    async def run(self):
        try:
            for file_from, file_to in self.from_to_dict.items():
                if self.current_file_changed is not None:
                    self.current_file_changed(file_to)
                await self.__copy_file_object(file_from, file_to)
        except asyncio.CancelledError as e:
            if self.cancelled_callback is not None:
                self.cancelled_callback()
        finally:
            if self.finish_callback is not None:
                self.finish_callback()

    async def __copy_file_object(self, file_from, file_to):
        async with AIOFile(file_from, 'rb') as fileFromObj:
            async with AIOFile(file_to, "wb+") as fileToObj:
                reader = Reader(fileFromObj, chunk_size=self.chunk_size)
                writer = Writer(fileToObj)
                async for chunk in reader:
                    await writer(chunk)
                    self.progress += len(chunk)
                    if self.progress_callback is not None:
                        self.progress_callback(Path(file_to).name, self.progress, self.max_progress)
                await fileToObj.fsync()
