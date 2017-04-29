file:"fact.txt"
%%
fact(float a){
    int fact = 1;
    int i = 1;
    int target = a;
    float res;
    if(a<=1.0){
        target = 1;
        i = 1; 
    }
    if(a>13.0){
        target = 13;
    }
    while(i<=target){
        fact = fact * i;
        i = i + 1;
    }
    res = fact;
    return res;
}