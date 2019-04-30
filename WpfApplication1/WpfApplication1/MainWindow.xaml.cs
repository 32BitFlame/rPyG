using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Collections.ObjectModel;
using System.IO;
using Microsoft.Win32;
using Newtonsoft.Json;
using Newtonsoft;
namespace WpfApplication1
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Hashtable mainRoomDictionary;
        public Dictionary<string, string> ProjectSolution;
        public string ProjectDirAbsPath = "";
        public ObservableCollection<Hashtable> roomJsons;
        public ObservableCollection<Room> rooms;
        public MainWindow()
        {
            InitializeComponent();
            roomJsons = new ObservableCollection<Hashtable>();
            rooms = new ObservableCollection<Room>();
            lb_Rooms.DataContext = rooms;
        }

        private void button_Click(object sender, RoutedEventArgs e)
        {
            //Exit App

            //Get Room Dir
            string currentDir = System.IO.Path.GetFullPath("rooms/");
            DirectoryInfo dirInfo = new DirectoryInfo(currentDir);
            
            //
            foreach(Hashtable d in roomJsons)
            {
                File.WriteAllText(d["Path"] as string, JsonConvert.SerializeObject(d));
            }
            Application.Current.Shutdown();
        }

        private void btn_CreateRoom_Click(object sender, RoutedEventArgs e)
        {
            roomJsons.Add(new Hashtable());
        }

        private void Btn_OpenProject_Click(object sender, RoutedEventArgs e)
        {
            //Create file dialouge for opening solution JSON
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "rPyG files (*.rpyg)|*.rpyg";
            if (openFileDialog.ShowDialog() == true)
            {
                //Deserialize Solution and change dir to solution directory
                ProjectSolution = JsonConvert.DeserializeObject<Dictionary<string, string>>(Convert.ToString(File.ReadAllText(openFileDialog.FileName)));
                Directory.SetCurrentDirectory(ProjectSolution["Dir"] as string);

                //Empty current rooms list and update new ones
                string currentDir = System.IO.Path.GetFullPath("rooms/");
                DirectoryInfo dirInfo = new DirectoryInfo(currentDir);
                Directory.SetCurrentDirectory(currentDir);
                roomJsons = new ObservableCollection<Hashtable>();
                foreach (FileInfo file in dirInfo.GetFiles())
                {
                    roomJsons.Add(JsonConvert.DeserializeObject<Hashtable>(File.ReadAllText(file.FullName)));
                }

                //Move back into main dir
                Directory.SetCurrentDirectory(ProjectSolution["Dir"] as string);

                foreach(Hashtable ht in roomJsons)
                {
                    Console.WriteLine(ht);
                    rooms.Add(new Room(ht));
                }
            }
            
        }

        private void CreateNewProject()
        {

        }

        private void Lb_Rooms_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            //Select new room
            mainRoomDictionary = lb_Rooms.SelectedItem as Hashtable;

            //Change Frame to mainRoom Editor
            RoomXAML roomDisp = new RoomXAML(mainRoomDictionary);

            RoomsViewer.Content = roomDisp;
        }
    }
}
