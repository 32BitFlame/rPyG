﻿using System;
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
using Newtonsoft.Json;
namespace WpfApplication1
{
    public class RoomDisp : SubWindow
    {
        private Frame SubWindowFrame;
        private List<object> Children;
        private dynamic jsonData;

        public RoomDisp(string jsondata, float width, float height) : base(height, width, "RoomDisp")
        {
            jsonData = JsonConvert.DeserializeObject(jsondata);
            SubWindowFrame.Width = width;
            SubWindowFrame.Height = height;

            Children.Add(new Page1(jsonData["Name"]));
        }

    }
}
