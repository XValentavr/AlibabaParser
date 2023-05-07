import asyncio
import concurrent.futures


class OneOffEventLoop:
    """ Exception safe event loop wrapper """

    def __enter__(self):
        self.loop = asyncio.new_event_loop()
        return self.loop

    def __exit__(self, *args):
        self.loop.close()


class GatherException(Exception):
    """ Gather exceptions from function of gather call into one raisable exception instance """

    def __init__(self, funcs, exceptions):
        self.funcs = funcs
        self.exceptions = exceptions

    def __str__(self):
        exc_str = "\n".join(
            (
                f"From function {f} got:\n{type(e).__name__}: {str(e)}"
                for f, e in zip(self.funcs, self.exceptions)
            )
        )
        return f"Got exception during gather call:\n{exc_str}"


def raise_on_exceptions(responses, funcs):
    """
    Raise exception on async thread pool
    """
    exceptions = []
    funcs_with_exceptions = []
    for fun, resp in zip(funcs, responses):
        if isinstance(resp, Exception):
            exceptions.append(resp)
            funcs_with_exceptions.append(fun)

    if len(exceptions) > 0:
        raise GatherException(funcs_with_exceptions, exceptions)


def run_in_threadpool(funcs, raise_on_first_exception=False):
    """ Run functions concurrently in threadpool and returns results

    Args
    funcs - list of functions to run. Wrap in functools.partial to glue arguments to them
    raise_on_first_exception - whether to raise on first exception happen, or wait until are collected
    """
    if len(funcs) == 0:
        return []
    return_exceptions = not raise_on_first_exception
    with OneOffEventLoop() as event_loop:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = event_loop.run_until_complete(
                asyncio.gather(
                    *(event_loop.run_in_executor(executor, func) for func in funcs),
                    return_exceptions=return_exceptions
                )
            )
            raise_on_exceptions(responses, funcs)
            return responses
