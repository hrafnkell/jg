<html>
<head>
    <title>Sérpöntunarlisti Járn og Gler</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">


    <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>

    <script src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
    <script>
        $(function() {
            $('#tooble').DataTable({
                "pageLength": -1,
                "lengthMenu": [[50, 100, -1], [50, 100, "All"]]
            });
        });
    </script>
</head>
<body>
<h1>Sérpöntunarlisti Járn og Gler - Improved!</h1>
Ratebeer einkunnir eru sóttar sjálfvirkt. Það er líklegt að einhverjir bjórar hafi ekki tengst við réttan bjór á RB og því með ranga einkunn/stíl. Hægt að klikka á RB score til að sannreyna það.
<table id="tooble">
    <thead><tr>
        <th>Vörunúmer</th>
        <th>Brugghús</th>
        <th>Nafn</th>
        <th>Stíll</th>
        <th>RB score</th>
        <th>Weighted</th>
        <th>RB ratings</th>
        <th>ABV</th>
        <th>ml</th>
        <th>Verð</th>
    </tr></thead>
    <tbody>
    <?php
    error_reporting(E_All);
    $dbh = new PDO('sqlite:beer.db');

    foreach($dbh->query("select b.stockid stockid, b.name name, b.price, br.name bname, b.size size, b.abv abv, rbratings, rbscore, rbweighed, rbid, s.name style from beers b LEFT OUTER JOIN breweries br ON b.brewery = br.rowid LEFT OUTER JOIN styles s ON s.rowid = b.rbstyle WHERE b.enabled = 1") as $row)
    {
        // brewery	stockid	name	price
        echo "<tr><td>{$row['stockid']}</td><td>{$row['bname']}</td><td>{$row['name']}</td><td>{$row['style']}</td><td><a href=\"http://www.ratebeer.com/beer/{$row['rbid']}/\">{$row['rbscore']}</th><th>{$row['rbweighed']}</a></td><td>{$row['rbratings']}</td><td>{$row['abv']}</td><td>{$row['size']}</td><td>{$row['price']}</td></tr>";
    }
    ?>
    </tbody>
</table>
Hver nennir eiginlega að leita í excel skjali? :)<br />
Kóði á <a href="https://github.com/hrafnkell/jg">github</a>.
</body>
</html>
