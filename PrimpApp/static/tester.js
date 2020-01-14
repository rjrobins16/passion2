var array = [ {'a': '12', 'b':'10'}, {'a': '20', 'b':'22'} ];

var r = array.map( x => {
    x.c = Number(x.b) - Number(x.a);
    return x
});

console.log(r);