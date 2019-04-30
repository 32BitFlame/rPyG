using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;
namespace WpfApplication1
{
    public class Room
    {
        private Hashtable Hasht;
        public string Name { get; }
        public Room(Hashtable ht)
        {
            Hasht = ht;
            Name = Hasht["Name"] as string;
        }
    }
}
