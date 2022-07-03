// Define vars representing HTMLDom
let IntrSct = document.querySelector('#IntrSct');  // <input id="IntrSct" type="range">
let Intr    = document.querySelector('#Intr');     // <span id="Intr">
let IntrClk = document.querySelector('#IntrClk');  // <button id="IntrClk">
let SpbrClk = document.querySelector('#SpbrClk');  // <button id="SpbrClk">

// Add event listeners
IntrSct.addEventListener('oninput', function()
{
  console.debug('Moved slider to ' + IntrSct.value);
  Intr.innerText = IntrSct.value;
});

IntrClk.addEventListener('click', function()
{
  chrome.tabs.getSelected(null, function(tab)
  {
    chrome.tabs.executeScript(tab.id, {
      code: 'window.freeRiceHackIntr = ' + IntrSct.value.toString() + ';'
    });

    chrome.tabs.executeScript(tab.id, {
      file: 'IntrClk.js',
    });
  });
});