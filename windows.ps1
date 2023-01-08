$compose = 'docker-compose up -d --scale serverweb=4'
$stop = 'docker-compose stop'
Invoke-Expression $compose
Invoke-Expression $stop
Invoke-Expression $compose
