using System;
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

namespace WpfApplication1
{
    public abstract class SubWindow
    {
        private Frame SubWindowFrame;
        private List<object> Children;
        public string Type { get; }
        public SubWindow(float height, float width, string type)
        {
            Type = type;
            SubWindowFrame.Width = width;
            SubWindowFrame.Height = height;
        }
        public Frame GetFrame() => SubWindowFrame;

        
    }
}
