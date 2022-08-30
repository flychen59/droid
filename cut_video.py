import cv2
import os
import shutil
import argparse





class image_process():
    def __init__(self,path_video_dir):

        self.path_video_dir=path_video_dir



        # self.frame_num=0



    # video_name = "0006"
    #
    # path_dir_save=r'C:\Users\flychen\Desktop\input\\'
    # path_dir=r'C:\Users\flychen\Desktop\input\Clip_Release_22-08-19\\'
    # path_dir1=r'C:\Users\flychen\Desktop\turn\crossroad\\'
    # path_dir2=r'C:\Users\flychen\Desktop\turn\onlyturn\\'
    # path_dir3=r'C:\Users\flychen\Desktop\turn\Yturn\\'
    # path_dir4=r'C:\Users\flychen\Desktop\pose\input_video_01-03\\'
    def cut_video(self,path_video_dir):
        frame_num_dic={}
        frame_size_dic={}
        video_name_list = []


        path_video=os.listdir(path_video_dir)
        for i in range(len(path_video)):
                video_name=path_video[i].split('.mp4')[0]
                video_name_list.append(video_name)
                output_dir_image = output_dir+'image_02/'
                current_working_dir = os.getcwd()
                print(current_working_dir)
                output_frame_dir=output_dir_image+video_name
                if not os.path.exists(output_frame_dir+'/'):
                    os.makedirs(output_frame_dir+'/')



                cap = cv2.VideoCapture(path_video_dir+video_name+'.mp4')


                frame_num=0
                print(cap.get(cv2.CAP_PROP_FPS))
                print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                while cv2.waitKey(33) < cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        cv2.imwrite(output_frame_dir+'/'+str(frame_num).zfill(4)+".png", frame)
                       # old_img_name=output_frame_dir+'/'+str(frame_num).zfill(4)+".png"
                       # new_file_name=output_frame_dir+'/'+str(frame_num).zfill(4)
                        # win
                        # cv2.imwrite(path_frame + "\\" + str(frame_num).zfill(4) + ".png", frame)
                        frame_num=frame_num+1
                        if frame_num==1:
                            output_frame_path = output_frame_dir + '/' + str(frame_num).zfill(4)+'.png'
                        #os.rename(old_img_name, new_file_name)

                    else:
                        break



                cap.release()
                cv2.destroyAllWindows()
                print("{0} frame_num:{1}".format(video_name, frame_num))


                # 合并成一个方法的多次使用
                key='frame_num{0}'.format(video_name)
                frame_num_dic[key]=frame_num

                img=cv2.imread(output_frame_path)
                key='{0} w:'.format(video_name)
                frame_size_dic[key]=img.shape[1]


                key = '{0} h:'.format(video_name)
                frame_size_dic[key]=img.shape[0]
        self.copyTxtCablib(video_name_list)
        self.makeCalib(video_name_list, frame_size_dic)

        self.copyTxtOxts(video_name_list)
        self.makeOxts(frame_num_dic)

        print(frame_num_dic,frame_size_dic)
        print(video_name_list)

        # print("frame_num:{0}".format(frame_num))
        # return frame_num_dic,frame_size_dic,video_name_list


    def copyTxtCablib(self,video_name_list):

        copy_dir_path="./originalData/calib/0000.txt"
        target_dir_path='./testing/calib'

        target_working_dir = self.make_dir(target_dir_path)

        for j in video_name_list:
            shutil.copy(copy_dir_path, target_working_dir + '/' + j)









    def makeCalib(self,video_name_list,frame_size_dic):

            path_calib = './testing/calib/'
            target_working_dir=self.make_dir(path_calib)
            for j in os.listdir(path_calib):
                # for k in video_name_list:
                    print(j)
                    key='{0} w:'.format(j)
                    key2='{0} h:'.format(j)
                    w = frame_size_dic[key]
                    h=frame_size_dic[key2]
                    f = 0.7 * w
                    f = '{0}'.format(f)
                    cx=0.5*w
                    cy=0.5*h


                    file_path = path_calib + j
                    file_data = ""
                    old_str1 = '1344'
                    new_str1 = '{0}'.format(f)
                    old_str2='960.0'
                    new_str2='{0}'.format(cx)
                    old_str3 = '544.0'
                    new_str3 = '{0}'.format(cy)

                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.replace(old_str1, new_str1)
                            line = line.replace(old_str2, new_str2)
                            line = line.replace(old_str3, new_str3)
                            file_data += line
                    with open(file_path, "w") as f:
                        f.write(file_data)
                
    def make_dir(self,path):
        current_working_dir = os.getcwd()
        target_working_dir = current_working_dir+path.split('.')[1]
        print(target_working_dir)
        if not os.path.exists(target_working_dir ):
            os.makedirs(target_working_dir )
        return target_working_dir


    def make_outputdir_root(self,data_path):
        root_list=['tracking','anns']
        
        for i in root_list:
            try:   
                os.makedirs(data_path+i)
            except:
                pass



    def copyTxtOxts(self,video_name_list):

        copy_dir_path="./originalData/oxts/0000.txt"
        output_dir_path='./testing/oxts/'

        target_working_dir=self.make_dir(output_dir_path)

        for j in video_name_list:
            shutil.copy(copy_dir_path,target_working_dir+'/'+j)

    def makeOxts(self,frame_num_dic):

        path_oxts = './testing/oxts/'
        target_working_dir=self.make_dir(path_oxts)
        for j in os.listdir(target_working_dir):
            z=j.replace('txt','')
            print(z)
            file_data = ''
            key = 'frame_num{0}'.format(z)
            frame_num = frame_num_dic[key]
            file_path = target_working_dir + z
            with open(file_path, "r") as f:
                for line in f:
                    print(line)
                    for n in range(frame_num):
                        file_data += line
            with open(file_path, "w") as f:
                f.write(file_data)
    def renameInOrder(dir_path):
        name_list_old = [x.split('.')[0] for x in sorted(os.listdir(dir_path))]



    # def move_dir(path_old,path_new):
    #     move_dir_old = './testing/'
    #     move_dir_new = './data/tracking/'
    #     shutil.move(move_dir_old, move_dir_new)













if __name__=='__main__':
    # path_video_dir='/home/flychen59/Desktop/qd3t/data/'
    # image_process.cut_video(path_video_dir)
    # copyTxt()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--path_video_dir',type=str)
    # parser.add_argument('--json_path_dir',type=str)
    # parser.add_argument('--output_dir',type=str)
    # args = parser.parse_args()
    parser = argparse.ArgumentParser()
    parser.add_argument('--outputName', required=True, type=str)
    args = parser.parse_args()
    data_path=os.getcwd()+'/data/'+args.outputName+'/'
    print(data_path)
    #if not os.path.exists(data_path):
    try:
        
        os.makedirs(data_path)
    except:
        pass
    image_process(1).make_outputdir_root(data_path)





    output_dir = './testing/'



    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path_video_dir='./inputdata/video_input/'
    json_path_dir='./inputdata/label_input/'
    

    image_process(path_video_dir).cut_video(path_video_dir)








    # os.system('cd')
    # os.system('python {0}'.format(label_path))
    # os.system("python ./lab_txt2.py")
    # label_txt.labelTxt()


    # def camera_para(self):
    #     with open(path) as r:
    #

