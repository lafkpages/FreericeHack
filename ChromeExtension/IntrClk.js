// Define the function
// Save it as a property of window to prevent re-defining variables if the extension is activated twice
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

  let correct = true;

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
  else
  {
    correct = false;
  }

  console.log(problem + ' = ' + answer + '\t%c' + (correct?'Correct':'Wrong'), ('color: ' + (correct?'green':'red') + ';'))

  for (let i = 0; i < window.bruh.length; i++)
  {
    clearTimeout(window.bruh[i]);
    bruh.shift();
  }

  bruh.push(setTimeout(window.freeRiceHackFunc, window.freeRiceHackIntr));
}

if (location.hostname.includes('freerice'))
{
  // Define a list to save all the timeouts
  // Save it as a property of window to prevent re-defining variables
  window.bruh = [];

  // Start the hack with an initial timeout, it will recall itself automatically
  bruh.push(setTimeout(window.freeRiceHackFunc, window.freeRiceHackIntr));
}
else
{
  console.info('The Freerice Hack extension was used on this page that is not Freerice.');
}