function csi = getcsi(array, len)
    csi = zeros(len,30,3);
    for j=1:len
        csi_one = get_scaled_csi(array{j});
        csi(j,:,:) = db(abs(squeeze(csi_one)'));
%         disp(size(db(abs(squeeze(csi_one)'))));
    end
end
