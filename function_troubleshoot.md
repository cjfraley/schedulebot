```
[3:42:47 PM] - Traceback (most recent call last):
  File "/layers/google.python.pip/pip/bin/functions-framework", line 8, in <module>
    sys.exit(_cli())
             ^^^^^^
  File "/layers/google.python.pip/pip/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/layers/google.python.pip/pip/lib/python3.11/site-packages/click/core.py", line 1078, in main

[3:42:47 PM] -     rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/layers/google.python.pip/pip/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/layers/google.python.pip/pip/lib/python3.11/site-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/layers/google.python.pip/pip/lib/python3.11/site-packages/functions_framework/_cli.py", line 37, in _cli
    app = create_app(target, source, signature_type)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/layers/google.python.pip/pip/lib/python3.11/site-packages/functions_framework/__init__.py", line 288, in create_app
    spec.loader.exec_module(source_module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/workspace/main.py", line 1, in <module>
    import yaml, json, csv
ModuleNotFoundError: No module named 'yaml'
```