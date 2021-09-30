self.onmessage = function (event) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", "http://" + event.data + ":5010/users", false ); // false for synchronous request
  xmlHttp.timeout = 500
  xmlHttp.ontimeout = function (e) {
    self.postMessage("Null")
    return "Null"
  };
  try{
    xmlHttp.send(null);
  }
  catch(err) {
    self.postMessage("Null")
    return "Null"
  }
  self.postMessage(xmlHttp.responseText);
  return xmlHttp.responseText
};