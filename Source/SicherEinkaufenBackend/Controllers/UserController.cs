using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Formatters;
using SicherEinkaufenBackend.Models;

namespace SicherEinkaufenBackend.Controllers
{

    [Route("api/[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        /// <summary>
        /// Get a TestUser
        /// </summary>
        /// <returns>User</returns>
        [HttpGet]
        [Produces("application/json")]
        [ProducesResponseType(typeof(User), 200)]
        public async Task<IActionResult> Get()
        {
          
            return Ok(new User() { UserName = "Peter" });
        }

        /// <summary>
        ///  Login a User 
        /// </summary>
        /// <param name="credentails"></param>
        /// <returns> success as a bool</returns>
        [HttpPost()]
        [Route("[action]")]
        [Produces("application/json")]
        [ProducesResponseType(typeof(bool), 200)]
        public async Task<IActionResult> Login(Credentails credentails)
        {
            //TODO: Implement me
            return Ok(true);
        }

        /// <summary>
        ///  Register a User
        /// </summary>
        /// <param name="credentails"></param>
        /// <returns>sucsess as a bool</returns>
        [HttpPost]
        [Route("[action]")]
        [Produces("application/json")]
        [ProducesResponseType(typeof(bool), 200)]
        public async Task<IActionResult> Register(Credentails credentails)
        {
            //TODO: Implement me
            return Ok(true);
        }

        /// <summary>
        /// Returns a userprofil
        /// </summary>
        /// <param name="token"></param>
        /// <returns>the userprofile for this token</returns>
        [HttpPost]
        [Route("[action]")]
        [Produces("application/json")]
        [ProducesResponseType(typeof(User), 200)]
        public  async Task<IActionResult> GetUserProfil(TokenModel token)
        {
            //TODO: Implement me
            return Ok(new User() { MarketID = 42, UserName = "Peter" });
        }

    }
}