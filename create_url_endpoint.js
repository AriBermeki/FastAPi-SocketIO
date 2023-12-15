/* 1 */


function formatiereURL(url) {
    // Überprüfe, ob die URL mit 'http://', 'https://', 'ws://' oder 'wss://' beginnt
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('ws://') || url.startsWith('wss://')) {
      return url; // Rückgabe der ursprünglichen URL, da sie bereits mit einem unterstützten Protokoll beginnt
    } else {
      // Wenn die URL keines der erwarteten Protokolle hat, füge das Protokoll von window.location.host hinzu
      return window.location.protocol+'//'+ window.location.host+ '/' + url;
    }
  }



/* 2 */
function formatiereURL(url) {
    const protokoll = /^(http:\/\/|https:\/\/|ws:\/\/|wss:\/\/)/;
    return url.match(protokoll) ? url : 'http://' + url;
}
  


/* 3 */
function formatiereURL(url) {
    const protokoll = /^(http:\/\/|https:\/\/|ws:\/\/|wss:\/\/)/;
    const mitProtokoll = url.match(protokoll) ? url : 'http://' + url;
  
    // Extrahiere das Protokoll
    const protokollTeil = mitProtokoll.match(protokoll)[0];
  
    // Hinzufügen von window.host und window.port, falls nicht vorhanden
    const vollstaendigeURL =
      mitProtokoll.includes(window.location.host) ?
      mitProtokoll :
      `${protokollTeil}${window.location.host}/${url.replace(protokoll, '')}`;
  
    return vollstaendigeURL;
  } 
  
  // Beispielaufrufe
  let url1 = 'example';
  let url2 = 'ws://example.com';
  let url3 = 'https://example.com';
  let url4 = 'wss://example.com';
  var result = formatiereURL(window.location.host);
  console.log(result)
  console.log(formatiereURL(url1)); // Ausgabe: http://127.0.0.1:5500/example.com
  console.log(formatiereURL(url2)); // Ausgabe: ws://127.0.0.1:5500/example.com
  console.log(formatiereURL(url3)); // Ausgabe: https://127.0.0.1:5500/example.com
  console.log(formatiereURL(url4)); // Ausgabe: wss://127.0.0.1:5500/example.com
