#!/usr/bin/env python

import argparse
import fileinput


class Language:
    def __init__(self, name, kinds):
        self.name = name
        self.kinds = set(kinds)

    def supported(self, tag):
        if self.__is_pseudo(tag):
            return False

        if self.__is_private(tag):
            return False

        return tag.kind in self.kinds

    def __is_pseudo(self, tag):
        return tag.name.startswith('!_TAG_')

    def __is_private(self, tag):
        return tag.name.startswith('__')


LANGUAGES = {
    None: Language(
        "Unknown",
        []
    ),
    'go': Language(
        'Golang',
        [
            'R',  # receiver
            'a',  # talias
            'f',  # func
            'i',  # interface
            'n',  # methodSpec
            's',  # struct
            't',  # type
        ]
    ),
    'js': Language(
        'Javascript',
        [
            'c',  # class
            'f',  # function
            'g',  # generator
            'm',  # method
            'v',  # variable
        ]
    ),
    'py': Language(
        'Python',
        [
            'I',  # namespace
            'c',  # class
            'f',  # function
            'm',  # member
            'v',  # variable
        ]
    ),
    "ts": Language(
        "Typescript",
        [
            'G',  # generator
            'c',  # class
            'f',  # function
            'i',  # interface
            'm',  # method
            'n',  # namespace
            'p',  # property
            'v',  # variable
        ]
    ),
    'sol': Language(
        'Solidity',
        []
    )
}


class Tag:
    def __init__(self, tag):
        self.fields = tag.split('\t')

    @property
    def supported(self):
        return self.language.supported(self)

    @property
    def name(self):
        return self.fields[0]

    @property
    def path(self):
        return self.fields[1]

    @property
    def excmd(self):
        return self.fields[2]

    @property
    def language(self):
        """Infer language from file extension."""
        return LANGUAGES.get(self.fields[1].split('.')[-1], LANGUAGES[None])

    @property
    def kind(self):
        return self.fields[3]

    @property
    def signature(self):
        return self.fields[-1].split(':')[-1] or ""

    def __repr__(self):
        return '\t'.join(self.fields)

    def __str__(self):
        if not self.supported:
            return

        return '\t'.join([
            # harded coded to g:fzf_layout in vimrc.
            self.name.ljust(32), self.path,
            self.excmd.rjust(56 - (len(self.path) + 8) // 8 * 8),
            self.signature.rjust(32)[:32]
        ])


if __name__ == '__main__':
    for line in fileinput.input():
        tag = Tag(line.rstrip())
        if tag.supported:
            print(tag)
