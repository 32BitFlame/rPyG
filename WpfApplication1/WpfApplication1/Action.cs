using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WpfApplication1
{
    public class Action
    {
        public string Name;
        public Hashtable ht;
        public Action(Hashtable hash)
        {
            ht = hash;
            Name = ht["Name"] as string;
        }
    }
}
