function f = fspecial (type, arg1, arg2)

  if (nargin < 1)
    print_usage ();
  endif

  switch lower (type)
    case 'average'
      if (nargin > 1 && isreal (arg1) && length (arg1 (:)) <= 2)
        fsize = arg1 (:);
      else
        fsize = 3;
      endif
      ## Create the filter
      f = ones (fsize);
      ## Normalize the filter to integral 1
      f = f / sum (f (:));

    case "disk"
      ## Get the radius
      if (nargin > 1 && isreal (arg1) && isscalar (arg1))
        r = arg1;
      else
        r = 5;
      endif
      ## Create the filter
      if (r == 0)
        f = 1;
      else
        ax = r + 1; # index of the "x-axis" and "y-axis"
        corner = floor (r / sqrt (2)+0.5)-0.5; # corner corresponding to 45 degrees
        rsq = r*r;
        ## First set values for points completely covered by the disk
        [X, Y] = meshgrid (-r:r, -r:r);
        rhi = (abs (X) +0.5).^2 + (abs (Y)+0.5).^2;
        f = (rhi <= rsq) / 1.0;
        xx = linspace (0.5, r - 0.5, r);
        ii = sqrt (rsq - xx.^2); # intersection points for sqrt (r^2 - x^2)
        ## Set the values at the axis caps
        tmp = sqrt (rsq -0.25);
        rint = (0.5*tmp + rsq * atan (0.5/tmp))/2; # value of integral on the right
        cap = 2*rint - r+0.5; # at the caps, lint = rint
        f(ax  ,ax+r) = cap;
        f(ax  ,ax-r) = cap;
        f(ax+r,ax  ) = cap;
        f(ax-r,ax  ) = cap;
        if (r == 1)
          y = ii(1);
          lint = rint;
          tmp = sqrt (rsq - y^2);
          rint = (y*tmp + rsq * atan (y/tmp))/2;
          val  = rint - lint - 0.5 * (y-0.5);
          f(ax-r,ax-r) = val;
          f(ax+r,ax-r) = val;
          f(ax-r,ax+r) = val;
          f(ax+r,ax+r) = val;
        else
          ## Set the values elsewhere on the rim
          idx = 1; # index in the vector ii
          x   = 0.5; # bottom left corner of the current square
          y   = r-0.5;
          rx  = 0.5; # x on the right of the integrable region
          ybreak = false; # did we change our y last time
          do
            i = x +0.5;
            j = y +0.5;
            lint = rint;
            lx = rx;
            if (ybreak)
              ybreak = false;
              val = lx-x;
              idx++;
              x++;
              rx = x;
              val -= y*(x-lx);
            elseif (ii(idx+1) < y)
              ybreak = true;
              y--;
              rx  = ii(y+1.5);
              val = (y+1) * (x-rx);
            else
              val = -y;
              idx++;
              x++;
              rx = x;
              if (floor (ii(idx)-0.5) == y)
                y++;
              endif
            endif
            tmp  = sqrt (rsq - rx*rx);
            rint = (rx*tmp + rsq * atan (rx/tmp))/2;
            val += rint - lint;
            f(ax+i, ax+j) = val;
            f(ax+i, ax-j) = val;
            f(ax-i, ax+j) = val;
            f(ax-i, ax-j) = val;
            f(ax+j, ax+i) = val;
            f(ax+j, ax-i) = val;
            f(ax-j, ax+i) = val;
            f(ax-j, ax-i) = val;
          until (y < corner || x > corner)
        endif
        # Normalize
        f /= pi * rsq;
      endif

    case "gaussian"
      ## fspecial ("gaussian", lengths = [3 3], sigma = 0.5)

      if (nargin < 2)
        lengths = [3 3];
      else
        validateattributes (arg1, {"numeric"}, {">", 0, "integer"},
                            "fspecial (\"gaussian\")", "LENGTHS");
        if (isempty (arg1))
          error ("fspecial (\"gaussian\"): LENGTHS must not be empty");
        elseif (numel (arg1) == 1)
          lengths = [arg1 arg1];
        else
          lengths = arg1(:).';
        endif
      endif

      if (nargin < 3)
        sigma = 0.5;
      else
        ## TODO add support for different sigmas for each dimension
        validateattributes (arg2, {"numeric"}, {">", 0, "scalar"},
                            "fspecial (\"gaussian\")", "SIGMA");
        sigma = arg2;
      endif

      lengths -= 1;
      lengths /= 2;
      pos = arrayfun ("colon", -lengths, lengths, "uniformoutput", false);
      dist = 0;
      for d = 1:numel(lengths)
        dist = dist .+ (vec (pos{d}, d) .^2); # broadcasting with '.+=' does not work
      endfor
      f = exp (- (dist) / (2 * (sigma.^2)));
      f /= sum (f(:));

    case "laplacian"
      ## Get alpha
      if (nargin > 1 && isscalar (arg1))
        alpha = arg1;
        if (alpha < 0 || alpha > 1)
          error ("fspecial: second argument must be between 0 and 1");
        endif
      else
        alpha = 0.2;
      endif
      ## Compute filter
      f = (4/(alpha+1))*[alpha/4,     (1-alpha)/4, alpha/4; ...
                         (1-alpha)/4, -1,          (1-alpha)/4;  ...
                         alpha/4,     (1-alpha)/4, alpha/4];
    case "log"
      ## Get hsize
      if (nargin > 1 && isreal (arg1))
        if (length (arg1 (:)) == 1)
          hsize = [arg1, arg1];
        elseif (length (arg1 (:)) == 2)
          hsize = arg1;
        else
          error ("fspecial: second argument must be a scalar or a vector of two scalars");
        endif
      else
        hsize = [5, 5];
      endif
      ## Get sigma
      if (nargin > 2 && isreal (arg2) && length (arg2 (:)) == 1)
        sigma = arg2;
      else
        sigma = 0.5;
      endif
      ## Compute the filter
      h1 = hsize (1)-1; h2 = hsize (2)-1; 
      [x, y] = meshgrid(0:h2, 0:h1);
      x = x-h2/2; y = y = y-h1/2;
      gauss = exp( -( x.^2 + y.^2 ) / (2*sigma^2) );
      f = ( (x.^2 + y.^2 - 2*sigma^2).*gauss )/( 2*pi*sigma^6*sum(gauss(:)) );

    case "motion"
      ## Taken (with some changes) from Peter Kovesis implementation 
      ## (http://www.csse.uwa.edu.au/~pk/research/matlabfns/OctaveCode/fspecial.m)
      ## FIXME: The implementation is not quite matlab compatible.
      if (nargin > 1 && isreal (arg1))
        len = arg1;
      else
        len = 9;
      endif
      if (mod (len, 2) == 1)
        sze = [len, len];
      else
        sze = [len+1, len+1];
      end
      if (nargin > 2 && isreal (arg2))
        angle = arg2;
      else
        angle = 0;
      endif
      
      ## First generate a horizontal line across the middle
      f = zeros (sze);
      f (floor (len/2)+1, 1:len) = 1;

      # Then rotate to specified angle
      f = imrotate (f, angle, "bilinear", "loose");
      f = f / sum (f (:));

    case "prewitt"
      ## The filter
      f = [1, 1, 1; 0, 0, 0; -1, -1, -1];
      
    case "sobel"
      ## The filter
      f = [1, 2, 1; 0, 0, 0; -1, -2, -1];
      
    case "kirsch"
      ## The filter
      f = [3, 3, 3; 3, 0, 3; -5, -5, -5];
    
    case "unsharp"
      ## Get alpha
      if (nargin > 1 && isscalar (arg1))
        alpha = arg1;
        if (alpha < 0 || alpha > 1)
          error ("fspecial: second argument must be between 0 and 1");
        endif
      else
        alpha = 0.2;
      endif
      ## Compute filter
      f = (1/(alpha+1))*[-alpha,   alpha-1, -alpha; ...
                          alpha-1, alpha+5,  alpha-1; ...
                         -alpha,   alpha-1, -alpha];

    otherwise
      error ("fspecial: filter type '%s' is not supported", type);
  endswitch
endfunction


