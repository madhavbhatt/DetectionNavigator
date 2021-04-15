function updateColor(){

    var mysql = require('/usr/local/lib/node_modules/mysql');

    var con = mysql.createConnection({
      host: "localhost",
      user: "django",
      password: "django-user-password",
      database: "mtnv"
    });

    con.connect(function(err) {
      if (err) throw err;
      var sql = "UPDATE mitrenv_techniques SET techColor='Red' WHERE techniqueName = 'T1529 : System Shutdown/Reboot';"
      con.query(sql, function (err, result) {
        if (err) throw err;
        console.log(result.affectedRows + " record(s) updated");
      });
    });

}