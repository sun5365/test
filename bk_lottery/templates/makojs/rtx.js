var rtxs = [];
% for item in rtxs:
    % if item.avatar is None:
        rtxs.push({name:'${item.name}',avatar:'${STATIC_URL}avatars/default.png'});
    % else:
        rtxs.push({name:'${item.name}',avatar:'${item.avatar}'});
    % endif
% endfor