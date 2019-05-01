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
    /// Interaction logic for Page1.xaml
    /// </summary>
    public partial class RoomXAML : Page
    {
        public ObservableCollection<Action> actions;
        public Hashtable JSON;
        public RoomXAML(Hashtable roomDict)
        {
            InitializeComponent();
            JSON = new Hashtable();
            this.JSON = roomDict;
            foreach(Hashtable ht in (this.JSON["Actions"] as Hashtable))
            {
                actions.Add(new Action(ht));
            }
            lb_Actions.DataContext = actions;
        }
        public void Refresh()
        {
            lbl_Head.Content = JSON["Name"];
        }
        public void Close()
        {
            JSON["intro"] = tb_InitalText.Text;
            File.WriteAllText(JSON["Path"] as string, JsonConvert.SerializeObject(JSON));
        }

        private void btn_Close_Click(object sender, RoutedEventArgs e)
        {
            MessageBoxResult WarningResult = MessageBox.Show("Are you sure you would like to delete", "WARNING", MessageBoxButton.YesNo);
            switch (WarningResult)
            {
                case MessageBoxResult.Yes:
                    //Delete Code
                    File.Delete(System.IO.Path.GetFullPath(JSON["Name"] as string));
                    MessageBox.Show("Deleted");
                    break;
                case MessageBoxResult.No:
                    break;
            }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }
    }
}
