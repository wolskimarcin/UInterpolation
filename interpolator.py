class Interpolator:

    @staticmethod
    def lagrange_interpolation(x, y, x_interp):
        # initialize list of interpolated y-values
        y_interp = []

        # loop over each interpolation point
        for xi in x_interp:
            # get interpolation value using Lagrange interpolation
            yi = 0
            for j in range(len(x)):
                # get all the x values except for xj
                x_others = x[:j] + x[j + 1:]
                # calculate L_j(x)
                lj = 1
                for xk in x_others:
                    lj *= (xi - xk) / (x[j] - xk)
                # add L_j(x) * y_j to yi
                yi += lj * y[j]
            # append yi to the list of interpolated y-values
            y_interp.append(yi)

        # return list of interpolated y-values
        return y_interp

    @staticmethod
    def cubic_spline_interpolation(x, y, x_interp):
        from scipy.interpolate import CubicSpline
        cs = CubicSpline(x, y)
        return cs(x_interp)

    @staticmethod
    def akima_spline_interpolation(x, y, x_interp):
        from scipy.interpolate import Akima1DInterpolator
        ai = Akima1DInterpolator(x, y)
        return ai(x_interp)

    @staticmethod
    def pchip_spline_interpolation(x, y, x_interp):
        # Piecewise Cubic Hermite Interpolating Polynomial (PCHIP)
        from scipy.interpolate import PchipInterpolator
        ai = PchipInterpolator(x, y)
        return ai(x_interp)
