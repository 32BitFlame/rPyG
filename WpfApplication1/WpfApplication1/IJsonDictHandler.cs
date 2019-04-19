using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WpfApplication1
{
    public interface IJsonDictDataHandler
    {
        Dictionary<string, string> Dict { get; set; }

        void Load(string fileAddress);

        Dictionary<string, string> Dump();

    }
}
