using System;
using System.IO;
using Microsoft.Win32;
namespace WpfApplication1
{
    public class DebugVars
    {
        public string SampleJSON;
        public DebugVars()
        {
            SampleJSON = File.ReadAllText("sample.json");

        }
    }
}