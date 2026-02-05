#!/bin/bash


echo site,transmitted,received,packet_loss,rtt_min,rtt_avg,rtt_max,rtt_mdev > res.csv

domains=(
  google.com yandex.ru
  github.com example.org
  stackoverflow.com wikipedia.org
  duckduckgo.com reddit.com
  cloudflare.com mozilla.org
  128.128.128.128
)

# пройдемся по доменам
for site in "${domains[@]}";
  do
  # пропингуем (-w=общий лимит выполнения, -W=лимит на каждый запрос)
  ping_info=$(ping -c3 -W2 $site)
  # результат выполнения последней команды
  exit_ping=$?

  # все сработало
  if [ $exit_ping -eq 0 ];
    then
    # дополнительные 3 параметра "transmitted,received,packet_loss"
    my_params=$(echo "$ping_info" | grep packets | sed 's|[%,]||g' | awk -v site="$site" '{print site","$1","$4","$6}')

    # нужные RTT параметры "rtt_min,rtt_avg,rtt_max,rtt_mdev"
    rtt_params=$(echo "$ping_info" | grep rtt | cut -d' ' -f4 | sed 's|/|,|g')
  else
    my_params="$site,0,0,100"
    rtt_params=",,,,"
  fi

# запишем в .csv формате
echo "$my_params,$rtt_params" >> res.csv

done