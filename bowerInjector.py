import sublime, sublime_plugin
import os,re,json

class bowerInjectorCommand(sublime_plugin.TextCommand):
    
    BASE_PATH = ''
    BOWER_PATH = ''
    BOWER_COMPONENTS_PATH = ''
    DS = os.sep

    def windowsDelimiter(self,location):
        if(self.DS =='\\'):
            new_location = location.replace('\\','\\\\')
            return new_location
        return location

    def normalizeLocation(self,location):
            not_ds = '\\' if (self.DS == '/') else '/'            
            return location.replace('./' ,'').replace(not_ds,self.DS)

    def getJSON(self,url):
        with open(url) as data_file:
            data = json.load(data_file)
            return data;

    def getDep(self,url):            
            data = self.getJSON(url) 
            dependencies = data['dependencies'];
            dep_folders = []

            for dep in dependencies:
                dep_folders += [dep] 
            return dep_folders

    def getMainAttr(self,folder):
        main = self.getJSON(self.BASE + folder+'/bower.json')
        return main["main"]


    def getMainAssets(self,folder):
            main = self.getMainAttr(folder)
            
            items = []   
            css   = []  
            js   = []  
        
            # check if main holds an array                    
            if (type(main) is list ):
                for m in main:            
                    f = folder + self.DS + self.normalizeLocation(str(m))  
                    items +=[f]                      
            else:
                items  += [folder + self.DS + self.normalizeLocation(str(main))]
            
            return items
    
    def orderFiles(self,files):
            js = []
            css = []
            
            if (type(files) is list ):
                for file in files:
                    matchObj = re.match(r'(.+?)\.js$',file,re.I)        
                    matchObj2 = re.match(r'(.+?)\.css$',file,re.I)        
                    if matchObj:                                                
                        js += [str(self.htmlReference('    ','js',self.BASE,matchObj.group()))]
                    elif(matchObj2):                        
                        css += [str(self.htmlReference('    ','css',self.BASE,matchObj2.group()))]
            else:                
                [str(htmlReference('    ','js',BASE,matchObj.group()))]

            return {"css":css,"js":js}            
      
    def htmlReference(self,space,type,base_url,file):
            if(type == 'js'):
                return space + '<script src="' + self.windowsDelimiter(base_url + file) + '"></script>'
            else:
                return space + '<link rel="stylesheet" href="' + self.windowsDelimiter(base_url + file) + '">'
    
    def getAll(self,url):
            css = []
            js  = []

            dependencies = self.getDep(url)
            for dep in dependencies:
                mainAssets = self.getMainAssets(dep)

                css += self.orderFiles(mainAssets)['css']
                js  += self.orderFiles(mainAssets)['js']
            return {"css":css,"js":js}   


    def run(self, edit):            
        
        filename = self.view.file_name() 
        
        BASE_PATH = filename.split(self.DS)
        del BASE_PATH[len(BASE_PATH)-1]
        self.BASE_PATH = str(self.DS.join(BASE_PATH))

        
        
        self.BOWER_PATH  = self.BASE_PATH + self.DS + "bower.json"
        self.BOWER_COMPONENTS_PATH  = self.BASE_PATH + self.DS + "bower_components" + self.DS 

  
        self.BASE = self.BASE_PATH + self.DS + 'bower_components' + self.DS 
        self.BASE_URL = self.BASE_PATH + self.DS + 'bower.json'
        
        
                  
        body = self.view.substr(sublime.Region(0, self.view.size()))
        
        newBody = re.sub(r"([\t ]*?)<!--[\t ]*bower:css[\t ]*-->([\s\S]*?)<\!--[\t ]*endbower[\t ]*-->",'<!-- bower:css -->\n' + str("\n".join(self.getAll(self.BASE_URL)['css'])) + '\n<!-- bower:end -->' ,body) 
        newBody = re.sub(r"([\t ]*?)<!--[\t ]*bower:js[\t ]*-->([\s\S]*?)<\!--[\t ]*endbower[\t ]*-->",'<!-- bower:js -->\n' + str("\n".join(self.getAll(self.BASE_URL)['js'])) + '\n<!-- bower:end -->' ,newBody)         
        
        ff = open(filename,'w')
        ff.write(newBody) 
        ff.close()
