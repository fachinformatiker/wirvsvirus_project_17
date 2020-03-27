using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace SicherEinkaufenBackend.Models
{
    public class MarketStatusBody
    {
        public string Token { get; set; }
        public int MarketID { get; set; }
        public int Status { get; set; }
    }
}
