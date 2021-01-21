from re import compile, match

regex = "^(?P<name>\w+) = BBox\('\w+', \((?P<tl0>\d+), (?P<tl1>\d+)\), \((?P<br0>\d+), (?P<br1>\d+)\), \((?P<cp0>\d+), (?P<cp1>\d+)\)\)"
    # (, (?P<tl1>\d+)), ((?P<br0>\d+), (?P<br1>\d+)), ((?P<cp0>\d+), (?P<cp1>\d+)))$"
line = "PVP_ON = BBox('PVP_ON', (522, 680), (544, 705), (544, 705))"

ma = match(regex, line)