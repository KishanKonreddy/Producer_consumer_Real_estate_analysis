"""
Stream utilities for lazy evaluation and functional transformations.
"""

from typing import Iterator, Callable, TypeVar, Iterable

T = TypeVar('T')
U = TypeVar('U')


def stream(data: Iterable[T]) -> Iterator[T]:
    """
    Create a generator stream from any iterable.
    Enables lazy evaluation of data.
    
    Args:
        data: Any iterable (list, tuple, etc.)
        
    Yields:
        Items from the iterable one at a time
    """
    for item in data:
        yield item


def stream_filter(predicate: Callable[[T], bool], data: Iterable[T]) -> Iterator[T]:
    """
    Lazy filter operation - only evaluates when consumed.
    
    Args:
        predicate: Function that returns True/False for each item
        data: Iterable to filter
        
    Yields:
        Items where predicate returns True
    """
    for item in data:
        if predicate(item):
            yield item


def stream_map(func: Callable[[T], U], data: Iterable[T]) -> Iterator[U]:
    """
    Lazy map operation - transforms items one at a time.
    
    Args:
        func: Transformation function
        data: Iterable to transform
        
    Yields:
        Transformed items
    """
    for item in data:
        yield func(item)


def stream_take(n: int, data: Iterable[T]) -> Iterator[T]:
    """
    Take first n items from stream (limit operation).
    
    Args:
        n: Number of items to take
        data: Iterable to limit
        
    Yields:
        First n items
    """
    count = 0
    for item in data:
        if count >= n:
            break
        yield item
        count += 1


def stream_skip(n: int, data: Iterable[T]) -> Iterator[T]:
    """
    Skip first n items from stream.
    
    Args:
        n: Number of items to skip
        data: Iterable to skip from
        
    Yields:
        Items after skipping n
    """
    count = 0
    for item in data:
        if count >= n:
            yield item
        count += 1


def stream_distinct(data: Iterable[T], key: Callable[[T], any] = None) -> Iterator[T]:
    """
    Remove duplicates from stream.
    
    Args:
        data: Iterable to deduplicate
        key: Optional function to extract comparison key
        
    Yields:
        Unique items
    """
    seen = set()
    for item in data:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            yield item


def stream_peek(action: Callable[[T], None], data: Iterable[T]) -> Iterator[T]:
    """
    Perform action on each item without consuming stream.
    Useful for debugging.
    
    Args:
        action: Function to call on each item
        data: Iterable to peek at
        
    Yields:
        Original items unchanged
    """
    for item in data:
        action(item)
        yield item