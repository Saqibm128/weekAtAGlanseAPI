fetch = require('node-fetch')

body = {
}
body = JSON.stringify(body)
fetch("http://40.76.22.123:8080/transaction/stats/ajax_all/splitByTime", {method:"POST", body:body})
        .then(resp=>resp.json())
        .then((respJson)=>{
          console.log(respJson)
          this.setState((state)=>respJson);
        })
