echotcpip('on',12345)
t = tcpip('localhost',12345);
fopen(t)

A = fread(t, 10);
disp(A)

fclose(t)
echotcpip('off')