from ihm.MyApp import MyApp
from nlquery import utils
#import subprocess

if __name__ == "__main__":
    #main(sys.argv[1:])
    #pour lancer automatiquement le stanford server
    #mais probleme au niveau du processus qui reste toujours actif
    #meme apres la fermeture de l'application
    #process = subprocess.Popen('cd stanford && java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer',shell=True)
    MyApp().mainloop()
    #process.kill()
    #print("process killed")
    
    #dataset1 = utils.loadDataset("dataset/annotated_wd_data_train.txt")
    #dataset2 = utils.loadDataset("dataset/qald-7-test-en-wikidata-withoutanswers.json")