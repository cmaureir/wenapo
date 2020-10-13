<img src="img/wenapo.png" width="400px" />

**W**rap **E**xtract **N**ormalize **A**nalyze **PO** files.

----

### Usage

To emulate `pospell` one can run `wenapo` with the `-p` and `-l` options:
`wenapo -p dict.txt -l es`.
Also, since the project uses [pyspellchecker](https://github.com/barrust/pyspellchecker)
we included an option `-s` to show the closes word as a suggestion,
since the process goes through the full original dictionary, it's a bit slow.

```
usage: wenapo [-h] [-p DICTIONARY] [-l LANGUAGE] [-s] po_file [po_file ...]

positional arguments:
  po_file

optional arguments:
  -h, --help            show this help message and exit
  -p DICTIONARY, --personal-dict DICTIONARY
                        Load a personal dictionary (default: dict.txt)
  -l LANGUAGE, --language LANGUAGE
                        Base language to use (default: es)
  -s, --suggestion      Suggest the closest word (slow) (default: False)
```


### Motivation

Have you tried to install and **use** `powrap` and `pospell` on Windows?

<img src="https://media1.giphy.com/media/13d2jHlSlxklVe/giphy.gif" width="300px" />

What usually starts as a simple `pip install powrap pospell` can end up in
a complicated process.

While translating the Python official documention to Spanish, we often had the
problem that Windows users were unable to locally run tools like `powrap` or
`pospell`.

With `powrap`, the problem was that apparently the default columns were not the
same on Git-bash (the only terminal where it works), this could be related to
the fact that Paths works different on that terminal, and on Windows in
general, but there were a lot of problems where on Linux and macOS the wrap
result was different compared to the one on Windows on Git-bash.  A common
issue for other terminals, like `CMD` was that `msgcat` the internal GNU tool
that `powrap` uses, failed since of course it's not available by default.

On the other hand, `pospell` internally uses Hunspell, so it will fail on the
first try after a `pip install`. You might think, well you can just install it?
Well, it's not so simple for someone that's starting with Python projects or
even Git related environments, I managed to make pospell work, by download the
package by [EZWinPorts](https://sourceforge.net/projects/ezwinports/) project,
and place it somewhere, and add the `bin/` directory to my `PATH`, in that case
`pospell` properly works.

I really believe that going to all this hazzle is too much for a project
that only requires you to translate text.
