# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-28 18:45:29
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-28 19:08:26
from dataclasses import dataclass


@dataclass
class Book:
    """Represent a book and its open or closed state."""

    title: str
    author: str
    pages: int
    is_open: bool = False

    def __post_init__(self) -> None:
        """Validate the book data after initialization."""
        if self.pages <= 0:
            raise ValueError("Las páginas deben ser un número positivo.")

    def show_info(self) -> None:
        """Display the book's current information."""
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages}")
        print(f"Open: {self.is_open}")

    def open(self) -> None:
        """Change the book's state to open."""
        self.is_open = True

    def close(self) -> None:
        """Change the book's state to closed."""
        self.is_open = False


def main() -> None:
    """Create a book and demonstrate its state changes."""
    book = Book(
        title="El Jardin de las Mariposas",
        author="Dot Hutchison",
        pages=280,
    )

    book.show_info()

    book.open()
    print("\nDespués de abrirlo:")
    book.show_info()

    book.close()
    print("\nDespués de cerrarlo:")
    book.show_info()


if __name__ == "__main__":
    main()
