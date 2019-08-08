import luigi
import os
import subprocess
from datetime import datetime

class MyTask(luigi.Task):
    
    bucket = luigi.Parameter()
    awsid = luigi.Parameter()
    awssecret = luigi.Parameter()
    region = luigi.Parameter()
    fileoutput = luigi.Parameter()


    def run(self):
        yield DownloadFiles(self.bucket)
        yield TaskPDF()
        yield TaskRTF()
        yield DeleteFiles()
        yield SendFiles(self.bucket)

    def requires(self):
        
        file_path = "/root/.aws/"
        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        login = "[default]\naws_access_key_id = {}\naws_secret_access_key = {}\n".format(self.awsid, self.awssecret)
        config = "[default]\nregion = {}\noutput = {}\n".format(self.region, self.fileoutput)
        arquivo = open('/root/.aws/credentials', 'w+')
        arquivo.write(login)
        arquivo.close()

        arquivo2 = open('/root/.aws/config', 'w+')
        arquivo2.write(config)
        arquivo2.close()


        

class DownloadFiles(luigi.Task):

    bucket = luigi.Parameter()
    data_atual = datetime.now()

    def output(self):
       return luigi.LocalTarget("/home/input/Download%s.txt" % self.data_atual)

    def requires(self):
        cmd = "aws s3 cp {} /home/input/ --recursive".format(self.bucket)
        push=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
        push.communicate()

        with self.output().open('w') as f:
            f.write('Download ok!')


class TaskPDF(luigi.Task):

    data_atual = datetime.now()


    def output(self):
        return luigi.LocalTarget("/home/input/PDF%s" % self.data_atual)

    def requires(self):
        cmd2 = "for FILE in $(find /home/input/ -name '*.pdf'); do pdftotext $FILE > $FILE.txt; done"
        push=subprocess.Popen(cmd2, shell=True, stdout = subprocess.PIPE)
        push.communicate()

        cmd3 = "find /home/input/ -name '*.pdf'"
        process = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
        #stdout = process.communicate()[0]

        with self.output().open('w') as f:
            while True:
                nextline = process.stdout.readline()
                if nextline == b'' and process.poll() != None:
                    break
                f.write(nextline.decode('utf-8'))

class TaskRTF(luigi.Task):

    data_atual = datetime.now()

    def output(self):
        return luigi.LocalTarget("/home/input/RTF%s" % self.data_atual)


    def requires(self):
        cmd3 = "for FILE in $(find /home/input/ -name '*.rtf'); do unrtf --text $FILE > $FILE.txt; done"
        push = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
        push.communicate()

        cmd4 = "find /home/input/ -name '*.rtf'"
        process = subprocess.Popen(cmd4, shell=True, stdout=subprocess.PIPE)

        with self.output().open('w') as f:
            while True:
                nextline = process.stdout.readline()
                if nextline == b'' and process.poll() != None:
                    break
                f.write(nextline.decode('utf-8'))

class DeleteFiles(luigi.Task):

    data_atual = datetime.now()

    def output(self):
        return luigi.LocalTarget("/home/input/Delete%s" % self.data_atual)

    def requires(self):
        cmd4 = "find /home/input/ -iname '*.pdf.txt' -exec rm {} \\;"
        push = subprocess.Popen(cmd4, shell=True, stdout=subprocess.PIPE)
        push.communicate()
        cmd5 = "find /home/input/ -iname '*.pdf' -exec rm {} \\;"
        push = subprocess.Popen(cmd5, shell=True, stdout=subprocess.PIPE)
        push.communicate()
        cmd6 = "find /home/input/ -iname '*.rtf' -exec rm {} \\;"
        push = subprocess.Popen(cmd6, shell=True, stdout=subprocess.PIPE)
        push.communicate()

        with self.output().open('w') as f:
            f.write('ok')


class SendFiles(luigi.Task):

    data_atual = datetime.now()
    bucket = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("/home/input/SendFile%s" % self.data_atual)

    def requires(self):

        bucket_temp = "%s" % self.bucket

        temp = bucket_temp.replace("s3://", "_")
        bucket_under = temp.replace("/", "_")

        file = "output%s.tar.gz" % bucket_under

        cmd7 = "tar -czvf "+file+" /home/input/"
        push = subprocess.Popen(cmd7, shell=True, stdout=subprocess.PIPE)
        push.communicate()



        cmd8 = "aws s3 cp " + file + " {}".format(self.bucket)

        push = subprocess.Popen(cmd8, shell=True, stdout=subprocess.PIPE)
        push.communicate()

        with self.output().open('w') as f:
            f.write('Bucket %s' % bucket_under)

