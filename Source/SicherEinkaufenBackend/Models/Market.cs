using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace SicherEinkaufenBackend.Models
{
    public class Market
    {
        public string Name { get; set; }
        public string Company { get; set; }
        public GPSLocation GPSLocation { get; set; }
        public string Adress { get; set; }
        public bool Enabled { get; set; }
        public int Status { get; set; }
    }

    public class GPSLocation
    {
        public long Lat { get; set; }
        public long Long { get; set; }
    }

}
