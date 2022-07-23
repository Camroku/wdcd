# wdcd
What da code doin'?

Pros:
* Just a single file, no bloat (except libraries :blush:).
* No too many files for configuration, just a single `.ini` file and you can keep them all in one place.

Cons:
* I felt too lazy to add support for every language.
* Images are not supported.
* Performance is a little too bad - it downloads an entire page on every request.
* You have to restart the server every time you change the configuration.

All of these will be fixed in future, except for the third one (probably?).

## Installing
Run `pip install flask requests beautifulsoup4` to install dependencies, move `wdcd.py` to `/usr/local/bin/wdcd` (`mv wdcd.py /usr/local/bin/wdcd`) and set it as executable (`chmod +x /usr/local/bin/wdcd`).

## Running
Create your config file by looking at the [example](config.ini) and then run `wdcd config.ini`.

## Credits
* [Arnolxu](https://github.com/Arnolxu) for the stylesheets (and literally making the project)
* [Prism](https://github.com/PrismJS) for syntax highlighting
