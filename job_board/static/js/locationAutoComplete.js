let baseURL = window.location.protocol + "//" + window.location.hostname;

var autoComplete = new autoComplete({
  selector: 'input[name="l"]',
  minChars: 1,
  source: function(term, response) {
    fetch(baseURL + `/locations?locationInp=${term}`)
      .then(response => response.json())
      .then(data => response(data));
  }
});
