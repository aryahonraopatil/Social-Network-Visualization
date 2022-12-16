import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;


boolean standalone = true;
boolean zoom = false;
int scale = 2;


// USE 1600x1200 RESOLUTION WHEN USING THE GLOBE
PImage myImage;
PShader magicPlanetShader, zoomShader;
PGraphics pg, layer;
PMatrix3D mat = new PMatrix3D(1.0,0.0,0.0,0.0,
                              0.0,1.0,0.0,0.0,
                              0.0,0.0,1.0,0.0,
                              0.0,0.0,0.0,1.0);

int currTime = 0;
int lastRotatedTime = 0;

boolean up;
boolean down;
boolean left;
boolean right; 
boolean spin;

String fileName;
String imageFile;

float xrot = 0;

List<Node> nodes;
Table node_table, links;

// GLTexture output;

void settings() {
  fullScreen(P2D, 2);
  //size(320, 240, P3D);
}

void setup() {
  nodes = new ArrayList<Node>();
  background(0, 0, 0);
  magicPlanetShader = loadShader("magicPlanetShader.glsl");
  zoomShader = loadShader("zoomShader.glsl");

  pg = createGraphics(height, height, P2D);
  layer = createGraphics(width, height, P2D);
  pg.textureWrap(CLAMP);
  pg.hint(DISABLE_TEXTURE_MIPMAPS);
  layer.textureWrap(CLAMP);
  layer.hint(DISABLE_TEXTURE_MIPMAPS);
  
  //CHANGE THIS TO TRUE TO  USE ON THE GLOVBE

  myImage = loadImage("media/mapBase.png");
  
  node_table = loadTable("../../datasets/accounts.csv", "header");
  links = loadTable("../../datasets/edges.csv", "header");
  
  for(TableRow row : node_table.rows()) {
    if(!(row.getString("lat").contains("_") || row.getFloat("lat") == 0))
      nodes.add(new Node(row.getFloat("lat"), row.getFloat("long"), row.getString("location"), row.getInt("follower_count"), row.getInt("DFC")));
  }
  
   // this is the code to add connections. Right now its just random
  for(TableRow row : links.rows())nodes.get(row.getInt("account")-1).connections.add(nodes.get(row.getInt("following")-1).pos);
  
  pg.smooth(8);
  layer.smooth(8);
  //colorMode(HSB, 360, 100, 100);
  //layer.colorMode(HSB, 360, 100, 100);
  //pg.colorMode(HSB, 360, 100, 100);
  frameRate(60);
  //mat.rotateX(.01);
  //mat.rotateY(.03);
}

void draw() {
  layer.beginDraw();
  layer.clear();
  Node last = null;
  for(Node n : nodes) {
    n.display(layer, last);
    last = n;
  }
  layer.endDraw();
  
  pg.beginDraw();
  if(xrot >= height) xrot -= height;
  if(xrot <= -height) xrot += height;
  
  for(int i = -1; i < 2; i++){
    pg.image(myImage, xrot + height*i, 0, height, height);
    pg.image(layer, xrot + height*i, 0, height, height);
  }
  // color based on proximity to root node or just base it off of following count
  // make color of the connection an average of the two node colors
  
  if(zoom) {
    zoomShader.set("scale", scale);
    pg.filter(zoomShader);
  }
  
  if (!standalone) {
    magicPlanetShader.set("rotation",mat,true);
    pg.filter(magicPlanetShader);  
  }
  
  pg.endDraw();
  
  if (!standalone) image(pg, (width-height)/2, 0, height, height);
  else               image(pg, 0, 0, height, height);
  
  
  if(up) mat.rotateY((millis()-lastRotatedTime)*-0.001);
  if(down)mat.rotateY((millis()-lastRotatedTime)*0.001);
  if(left) xrot += (millis()-lastRotatedTime)*-0.1;
  if(right) xrot += (millis()-lastRotatedTime)*0.1;
  
  if(spin) xrot += (millis()-lastRotatedTime)*0.12;
  
  lastRotatedTime = millis();
}

void keyPressed() {
  if (key == CODED) {
    if ((keyCode == LEFT)||(keyCode == 16)||(keyCode == 37)) {
          left = true;
          lastRotatedTime = millis();
    }
    
    if ((keyCode == RIGHT)||(keyCode == 11)||(keyCode == 39)) {
          right = true;
          lastRotatedTime = millis();
    }
    
    if ((keyCode == UP)||(keyCode == 38)){
          up = true;
          lastRotatedTime = millis();
    }
    
    if ((keyCode == DOWN)||(keyCode == 40)){
          down = true;
          lastRotatedTime = millis();
    }
  }
  if (keyCode == 80){
      spin = !spin;
      lastRotatedTime = millis();
    }
}

void keyReleased(){
    if ((keyCode == LEFT)||(keyCode == 16)||(keyCode == 37)) left = false;
    
    if ((keyCode == RIGHT)||(keyCode == 11)||(keyCode == 39)) right = false;

    if ((keyCode == UP)||(keyCode == 38)) up = false;
    
    if ((keyCode == DOWN)||(keyCode == 40)) down = false;
}
