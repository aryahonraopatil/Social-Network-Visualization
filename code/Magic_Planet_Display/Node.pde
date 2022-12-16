class Node {
  Point pos;
  String handle, time, locName;
  color c;
  int followers;
  ArrayList<Point> connections;
  Node(float lat, float lon, String locName, int followers, int hops){
    connections = new ArrayList<Point>();
    setLatLon(lat, lon);
    this.followers = followers;
    this.locName = locName;
    // HSB with this might look cooler
    print(hops);
    switch(hops) {
      case 0:
        c = color(180, 20, 20);
        break;
      case 1:
        c = color(180, 40, 76);
        break;
      case 2:
        c = color(20, 180, 20);
        break;
      case 3:
        c = color(20, 20, 180);
        break;
      case 4:
        c = color(100, 20, 180);
        break;
      default:
        c = color(180, 20, 20);
        break;
    }
  }
  
  void addConnection(Node n){
    connections.add(n.pos);
  }
  
  void setLatLon(float lat, float lon) {
    pos = new Point((lon+180f)/360f, 1.2*log(tan(PI/4f + .5*radians(lat))));
    pos.x*= layer.width;
    pos.y = layer.height/2 - layer.height*pos.y/4;
  }
  
  void display(PGraphics layer, Node last) {
    //c = color((hue(c) + 1)%180, green(c), blue(c));
    //pg.point(pos.x, pos.y);
    layer.strokeWeight(4 + (followers/150.0));
    layer.stroke(c);
    layer.point(pos.x, pos.y);
    layer.strokeWeight(1);
    if(last != null) {
      if(true);// check to see if its faster to go around the edge, TODO
      layer.line(pos.x, pos.y, last.pos.x, last.pos.y);
    }
  }
}

class Point {
  float x, y;
  
  Point(float x, float y){
    this.x = x;
    this.y = y;
  }
  
  float dist(float x2, float y2){
    return sqrt((x2-x)*(x2-x) + (y2-y)*(y2-y));
  }
}
