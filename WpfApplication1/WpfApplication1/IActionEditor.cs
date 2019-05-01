  
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
  public interface IActionEditor 
  {
    private Hashtable InputToData;
    public Hashtable roomDictionary;
    public Hashtable ActionDictionaryKey;
    public void Close();
  }
}
