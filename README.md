Bogus Test Server
=================

This server is aimed for test only.
If your code talks with any REST api this is your project, you can fake any responses
the way you like, but by default it will return 200 to any url you request.

Mocking any HTTP request
------------------------

```python
b = Bogus() # creates a bogus instance but doesn't starts the server.
b.register("/index.html", lambda: ("your response body", 201)) # the handler registered must return both parameters.
url = b.serve() # this returns the server's url, but it also is accessible in the bogus object `url` property.
```

With this done you'll have a server that receives any requests returning 200,
but when someone asks specifically for `/index.html` it'll return your response and status code
as defined in your function.

You can also pass parameters to a request and receive them in your handler:

#TODO: review how to register endpoints that receive parameters in url
```python
b = Bogus()
b.register("/search", lambda x: ("Your search for {} didn't find anything".format(x), 200))
b.serve()
```

This will do the same as before, but if you don't pass a parameter to the `/search` endpoint
Bogus will give a 400 Bad Request response.

If you want to serve only a set of endpoints in your server just pass the `promiscuous=False`
flag to the constructor, e.g.:

```python
b = Bogus(promiscuous=False)
b.serve()
```

This is just an example, if you do that Bogus server will respond 404 for every request,
since there's no handler registered to deal with anything.
As you may guessed this flag is True by default.
