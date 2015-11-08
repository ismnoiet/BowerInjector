# sublime3-bower-Injector
A sublime text 3 plugin that inject all bower dependencies
in the **index.html** page of the current project


## dependencies
you should have python 3 already installed on your machine

## Installation
In order to install this plugin you have two options,
the manual option and the package control one(will be available very soon)

### manually
You can easily install this plugin manually, simply download the zip file and extract it to sublime text   **Packages** folder

### Package Control
It will be released soon

## How does it work ?
Now the plugin is installed and ready to be used.
Let's say that you have a project organised like the following:

```
myProject/
├── otherStuff/
├── bower_components/
│   ├── jquery/
│   ├── bootstrap/
│   └── ...
│
├── bower.json  
└── index.html
```

simply add **bower:css** or **bower:js** to **index.html** depending on what you want to load, generally we want to load them both some we end up with something like that :

```
<html>
  <head>
      <!-- load css files -->

      <!-- bower:css -->
      <!-- endbower -->

  </head>

  <body>
    <!-- body content goes here -->
    <!-- load js files -->

    <!-- bower:js -->
    <!-- endbower -->

  </body>
</html>
```

then hit **ctrl + y** ( you can change the key ) to execute the plugin
