p2 = 48; p3 = 1; 
siz   = (p2-1)/2;
 std2   = p3^2;

 [x,y] = meshgrid(-siz(1):siz(1),-siz(1):siz(1));
 arg   = -(x.*x + y.*y)/(2*std2);

 h     = exp(arg);
 h(h<eps*max(h(:))) = 0;

 sumh = sum(h(:));
 if sumh ~= 0,
   h  = h/sumh;
 end;
 % now calculate Laplacian     
 h1 = h.*(x.*x + y.*y - 2*std2)/(std2^2);
 h     = h1 - sum(h1(:))/prod(p2)
 size(h)