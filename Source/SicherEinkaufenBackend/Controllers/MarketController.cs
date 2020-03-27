﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using SicherEinkaufenBackend.Models;

namespace SicherEinkaufenBackend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MarketController : ControllerBase
    {
        /// <summary>
        ///  Returns a List of all Markets
        /// </summary>
        /// <returns></returns>
        [HttpGet]
        [Produces("application/json")]
        [ProducesResponseType(typeof(List<Market>), 200)]

        public async Task<IActionResult> Get()
        {
            List<Market> markets = new List<Market>() { new Market() { Name = "PeterMark" }, new Market { Name = "MegaMarkt" } };
            return Ok(markets);
        }

        /// <summary>
        /// Returns a specific Market
        /// </summary>
        /// <param name="id"></param>
        /// <returns></returns>
        [HttpGet]
        [Produces("application/json")]
        [ProducesResponseType(typeof(Market), 200)]

        public async Task<IActionResult> Get(int id)
        {
            return Ok(new Market() { Name = "PeterMark" });
        }

        /// <summary>
        /// Creates a new market
        /// </summary>
        /// <param name="market"></param>
        /// <returns>sucsess as a bool</returns>
        [HttpGet]
        [Produces("application/json")]
        [ProducesResponseType(typeof(bool), 200)]

        public async Task<IActionResult> GetMarketList(Market market)
        {
            return Ok();
        }

        /// <summary>
        /// Creats new Market 
        /// </summary>
        /// <param name="market"></param>
        /// <returns></returns>
        [HttpPost]
        [Produces("application/json")]
        [ProducesResponseType(typeof(bool), 200)]

        public async Task<IActionResult> CreateMarket(Market market)
        {
            return Ok(true);
        }

        /// <summary>
        /// Sets Status of a Market
        /// </summary>
        /// <param name="marketStatusBody"></param>
        /// <returns></returns>
        [HttpPut]
        [Produces("application/json")]
        [ProducesResponseType(typeof(bool), 200)]

        public async Task<IActionResult> SetMarketStatus(MarketStatusBody marketStatusBody)
        {
            return Ok(true);
        }
    }
}