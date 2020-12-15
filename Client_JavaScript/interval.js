//      _______              ____  _              ____        __ 
//     / _____/ ___         / __ \(_)_______     / __ )____  / /_
//    / /__   / __/        / /_/ / / ___/ _ \   / __  / __ \/ __/
//   / ___/  / /          / _, _/ / /__/  __/  / /_/ / /_/ / /_  
//  /_/     /_/          /_/ |_/_/\___/\___/  /_____/\____/\__/  
//  
//  Original by: Neil Master/Yeehawlerz101
//  Remixed by: LuisAFK
//  Notes: Make sure to leave your ad blocker off so that 'freerice' can have some sort of income :)
//  How to use: Make an account, sign in, then go to the multiplacation table category (freerice.com/categories/multiplication-table)
//  Then when the page loads, go to the console of your web browser and paste this code in the console and enjoy!
//  https://github.com/lafkpages/FreericeHack



// Define the function
// Save it as a property of window to prevent re-defining variables
window.freeRiceHackFunc = function()
{ 
  let problem = document.getElementsByClassName("card-title")[0].innerText;   // '11 x 12'
  let pr      = problem.replace('x', '*');                                    // '11 * 12'

  let answer = eval(pr);                                                      // 132

  let opts = document.getElementsByClassName('card-button');                  // [HTMLElement, HTMLElement, HTMLElement, HTMLElement]

  let a = opts[0];                                                            // HTMLElement
  let b = opts[1];                                                            // HTMLElement
  let c = opts[2];                                                            // HTMLElement
  let d = opts[3];                                                            // HTMLElement

  if (parseInt(a.innerText) == answer)
  {
    a.click();
  }
  else if (parseInt(b.innerText) == answer)
  {
    b.click();
  }
  else if (parseInt(c.innerText) == answer)
  {
    c.click();
  }
  else if (parseInt(d.innerText) == answer)
  {
    d.click();
  }

  for (let i = 0; i < window.bruh.length; i++)
  {
    clearTimeout(window.bruh[i]);
    bruh.shift();
  }

  bruh.push(setTimeout(window.freeRiceHackFunc, 400));
}

// Define a list to save all the timeouts
// Save it as a property of window to prevent re-defining variables
window.bruh = [];

// Start the hack with an initial timeout, it will recall itself automatically
bruh.push(setTimeout(window.freeRiceHackFunc, 400));