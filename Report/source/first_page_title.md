<!-- Add this code inside the template in the section 'header and footer'
\newpairofpagestyles{footer-only}{
    \clearpairofpagestyles
    \setheadsepline{0pt}
    \setfootsepline{.4pt}
    \ifoot*{$if(footer-left)$$footer-left$$else$$for(author)$$author$$sep$, $endfor$$endif$}
    \cfoot*{$if(footer-center)$$footer-center$$else$$endif$}
    \ofoot*{$if(footer-right)$$footer-right$$else$\thepage$endif$}
    \addtokomafont{pageheadfoot}{\upshape}
} 
-->

\thispagestyle{footer-only}

\begin{center}
\textbf{\Large \thetitle} \\
\theauthor
\end{center}
\vspace{1em}
