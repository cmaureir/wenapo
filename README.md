# wenapo

**W**rap **E**xtract **N**ormalize **A**nalyze **PO** files.

Have you tried to install and **use** `powrap` and `pospell` on Windows?

<img src="https://media1.giphy.com/media/13d2jHlSlxklVe/giphy.gif" width=150px />

What usually starts as a simple `pip install powrap pospell` can end up in
a complicated process.

### Motivation

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
