const canvas = document.getElementById('canvas1')
const c = canvas.getContext('2d')
canvas.width = window.innerWidth//1024
canvas.height = window.innerHeight //576
c.lineWidth = 2;
const gradient = c.createLinearGradient(0, 0, canvas.width, canvas.height);
gradient.addColorStop(0, 'yellow');
gradient.addColorStop(0.5, 'magenta');
gradient.addColorStop(1, 'red');
c.fillStyle = gradient;

class Particle{
    constructor(effect){
        this.effect = effect;
        this.radius = 2 + 5*Math.random();
        this.x = this.radius+Math.random()*(this.effect.width-this.radius);
        this.y = this.radius+Math.random()*(this.effect.height-this.radius);
        this.vx = Math.random()-0.5;
        this.vy = Math.random()-0.5;
        if(this.vx > 0)this.vx+=0.1;
        else this.vx-=0.1;
        if(this.vy > 0)this.vy+=0.1;
        else this.vy-=0.1;
    }
    draw(context){
        // context.fillStyle = `hsl(${this.x*0.25}, 100%, 50%)`
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, Math.PI*2);
        context.fill();
    }
    update(){
        if(this.x > this.effect.width-this.radius || this.x < this.radius)this.vx*=-1;
        if(this.y > this.effect.height-this.radius || this.y < this.radius)this.vy*=-1;

        this.x+=this.vx;
        this.y+=this.vy;
        // this.y+=this.vy;
        if(this.effect.mouse.pressed=true){
            const distMouse = distance(this.x, this.y, this.effect.mouse.x, this.effect.mouse.y)
            if(distMouse < this.effect.mouse.radius){
                const angle = Math.atan2(this.y-this.effect.mouse.y, this.x-this.effect.mouse.x)
                const proximity = 1-distMouse/this.effect.mouse.radius
                const thrust = 5.0
                // const v_mag = Math.sqrt(this.vx**2 + this.vy**2)
                // this.vx = v_mag*Math.cos(angle)
                // this.vy = v_mag*Math.sin(angle)
                this.x += Math.cos(angle)*thrust*proximity
                this.y += Math.sin(angle)*thrust*proximity
                this.bounce();
            }
        }
    }
    bounce(){
        if(this.x < this.radius)this.x=this.radius;
        if(this.y < this.radius)this.y=this.radius;
        if(this.x > this.effect.width-this.radius)this.x=this.effect.width-this.radius;
        if(this.y > this.effect.height-this.radius)this.y=this.effect.height-this.radius;
    }
    squared_distance(particle){
        return (this.x-particle.x)**2 + (this.y-particle.y)**2;
    }
}

class Effect{
    constructor(canvas, context){
        this.canvas = canvas;
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        this.particles = [];
        this.numberOfParticles = 200;
        this.gradient = context.createLinearGradient(0, 0, this.width, this.height);
        this.gradient.addColorStop(0, 'yellow');
        this.gradient.addColorStop(0.5, 'magenta');
        this.gradient.addColorStop(1, 'red');
        context.fillStyle = this.gradient;
        this.createParticles();

        this.mouse = {
            x: 0,
            y: 0,
            pressed: false,
            radius: 150
        }

        window.addEventListener('resize', e=>{
            this.resize(e.target.window.innerWidth, e.target.window.innerHeight, context)
        });
        window.addEventListener('mousemove', e=>{
            this.mouse.x = e.x;
            this.mouse.y = e.y;
        });
        window.addEventListener('mousedown', e=>{
            this.mouse.pressed = true;
        });
        window.addEventListener('mouseup', e=>{
            this.mouse.pressed = false;
        });

    }
    createParticles(){
        for(let i=0; i<this.numberOfParticles; i++){
            this.particles.push(new Particle(this));
        }
    }
    handleParticles(context){
        context.fillStyle = this.gradient;
        this.particles.forEach((particle)=>{
            particle.draw(context);
            particle.update();
        })
        this.connectParticles(context);
    }
    connectParticles(context){
        const maxDistance = 100;
        context.strokeStyle  = this.gradient;
        for(let i=0; i<this.particles.length; i++){
            for(let j=i; j<this.particles.length; j++){
                const distBtwParticles = distance(this.particles[i].x, this.particles[i].y, 
                    this.particles[j].x, this.particles[j].y);
                if(distBtwParticles<maxDistance){
                    context.save()
                    const opacity = 1.2 - distBtwParticles/maxDistance;
                    context.globalAlpha = opacity;
                    context.beginPath();
                    context.moveTo(this.particles[i].x, this.particles[i].y);
                    context.lineTo(this.particles[j].x, this.particles[j].y);
                    context.stroke();
                    context.restore()
                }
            }
        }
    }
    resize(width, height, context){
        this.canvas.width = width;
        this.canvas.height = height;
        this.width = width;
        this.height = height;

        this.gradient = context.createLinearGradient(0, 0, width, height);
        this.gradient.addColorStop(0, 'yellow');
        this.gradient.addColorStop(0.5, 'magenta');
        this.gradient.addColorStop(1, 'red');

        for(let i=0; i<this.particles.length; i++){
            if(this.particles[i].x > width-this.particles[i].radius)this.particles[i].x=width-this.particles[i].radius;
            if(this.particles[i].y > height-this.particles[i].radius)this.particles[i].y=height-this.particles[i].radius;
        }
    }
}

const effect = new Effect(canvas, c);

function animate(){
    window.requestAnimationFrame(animate)
    c.fillStyle = 'white'
    c.fillRect(0, 0, canvas.width, canvas.height)
    c.restore() 
    //ANIMATE 
    // c.fillStyle = gradient;
    effect.handleParticles(c);
}
animate()

function distance(x1, y1, x2, y2){
    return Math.hypot(x1-x2, y1-y2);
}

window.addEventListener("scroll", function() {
    const box = document.querySelector(".homepage");
    const texts = document.querySelectorAll(".scroll-text");
    const scrollPosition = window.scrollY;
    const backgroundColor = `rgba(0, 0, 0, ${Math.min(0.1 + scrollPosition / 1000, 1)})`;
    const textColor = `hsl(24, 100%, ${Math.min(100, scrollPosition / 5)}%)`;
    box.style.backgroundColor = backgroundColor;
    texts.forEach((text)=>{
        text.style.color = textColor;
    })
    console.log(textColor)
  });