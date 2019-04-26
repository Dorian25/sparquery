from ihm.MyApp import MyApp
import subprocess

if __name__ == "__main__":
    #main(sys.argv[1:])
    
    process = subprocess.Popen('cd stanford && java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer',shell=True)
    MyApp().mainloop()