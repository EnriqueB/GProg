file:"pow.txt"
%%
pow(float a, float b){
    int times = b;
    int i = 0;
    float total = 1.0;
    if(b<1.0){
        b = 1.0;
    }
    if(b>=10){
        b = 9.0;
    } 
    while(i<b){
        total = total * a;
        i = i + 1;
    }
    return total;
}